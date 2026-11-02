"""Bounded HTTPS downloads and ZIP member range reads; no remote code execution."""
from __future__ import annotations

import hashlib
import io
import re
import struct
import time
import urllib.request
import zipfile
import zlib
from pathlib import Path
from urllib.parse import urlsplit

from agent.run_agent import require, stamp

HOSTS = {"zenodo.org", "phm-datasets.s3.amazonaws.com"}


def sha256(path):
    with Path(path).open("rb") as f:
        return hashlib.file_digest(f, "sha256").hexdigest()


class SourceRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        require(urlsplit(newurl).scheme == "https" and
                urlsplit(newurl).hostname == urlsplit(req.full_url).hostname,
                "Unexpected source redirect")
        return super().redirect_request(req, fp, code, msg, headers, newurl)


def download(url, destination, limit, byte_range=None, deadline_seconds=240):
    """Two attempts, socket timeout, wall-clock deadline, hard byte cap."""
    require(urlsplit(url).scheme == "https" and urlsplit(url).hostname in HOSTS,
            "Source is not allowlisted")
    destination = Path(destination)
    destination.parent.mkdir(parents=True, exist_ok=True)
    part = destination.with_name(destination.name + ".part")
    started = time.monotonic()
    error = None
    for attempt in range(2):
        try:
            headers = {"User-Agent": "X6-research-agent/2", "Accept-Encoding": "identity"}
            if byte_range:
                headers["Range"] = "bytes=" + byte_range
            request = urllib.request.Request(url, headers=headers)
            opener = urllib.request.build_opener(SourceRedirect)
            with opener.open(request, timeout=45) as response:
                require(response.status == (206 if byte_range else 200),
                        "Server did not honour required HTTP response/range")
                length = response.headers.get("Content-Length")
                require(length is None or int(length) <= limit, "Download exceeds byte cap")
                n = 0
                with part.open("wb") as f:
                    while True:
                        require(time.monotonic() - started < deadline_seconds, "Download deadline exceeded")
                        block = response.read(min(1024 * 1024, limit - n + 1))
                        if not block:
                            break
                        n += len(block)
                        require(n <= limit, "Download exceeds byte cap")
                        f.write(block)
                require(n > 0 and (length is None or n == int(length)), "Truncated/empty download")
                metadata = {"url": url, "retrieved_at": stamp(), "http_status": response.status,
                            "bytes": n, "range": byte_range,
                            "content_range": response.headers.get("Content-Range"),
                            "etag": response.headers.get("ETag"), "attempts": attempt + 1}
            part.replace(destination)
            metadata["sha256"] = sha256(destination)
            return metadata
        except Exception as exc:
            error = exc
            part.unlink(missing_ok=True)
            if attempt == 0 and time.monotonic() - started < deadline_seconds:
                time.sleep(2)
            else:
                break
    raise RuntimeError(f"Source download failed: {type(error).__name__}: {error}")


def read_zip_member(url, member, destination, work, expected_sha256):
    """Read central directory and one <16 MB ZIP member, never the 1.2 GB archive.

    Supports the verified non-ZIP64 Zenodo archive layout. A layout change fails
    explicitly; CRC and pinned member SHA-256 both have to match.
    """
    work = Path(work)
    tail_path = work / "zip-tail.bin"
    tail_meta = download(url, tail_path, 65536, "-65536")
    tail = tail_path.read_bytes()
    match = re.fullmatch(r"bytes (\d+)-(\d+)/(\d+)", tail_meta["content_range"] or "")
    require(match is not None, "Missing archive Content-Range")
    begin, end, total = map(int, match.groups())
    require(end + 1 == total and end - begin + 1 == len(tail), "Invalid archive tail range")
    # zipfile adjusts offsets relative to this tail buffer; adding begin restores them.
    with zipfile.ZipFile(io.BytesIO(tail)) as archive:
        entry = archive.getinfo(member)
        require(0 < entry.file_size <= 16_000_000 and 0 < entry.compress_size <= 16_000_000,
                "ZIP member exceeds size budget")
        require(not entry.flag_bits & 1 and entry.compress_type == zipfile.ZIP_DEFLATED,
                "Unsupported ZIP member encoding")
        offset = entry.header_offset + begin
        count = entry.compress_size + 4096
        require(0 <= offset < offset + count <= total, "ZIP member range outside archive")
        packed_path = work / "zip-member.bin"
        packed_meta = download(url, packed_path, count, f"{offset}-{offset + count - 1}")
        require(packed_meta["content_range"] == f"bytes {offset}-{offset+count-1}/{total}",
                "Wrong ZIP member range returned")
        packed = packed_path.read_bytes()
        header = struct.unpack("<4s5H3I2H", packed[:30])
        require(header[0] == b"PK\x03\x04" and header[3] == entry.compress_type,
                "ZIP local header mismatch")
        name_size, extra_size = header[-2:]
        require(packed[30:30+name_size].decode("utf-8") == member, "Wrong ZIP member name")
        start = 30 + name_size + extra_size
        require(start <= 4096, "ZIP local header too large")
        decoder = zlib.decompressobj(-15)
        raw = decoder.decompress(packed[start:start+entry.compress_size], entry.file_size + 1)
        require(decoder.eof and not decoder.unconsumed_tail and len(raw) == entry.file_size,
                "ZIP decompression size mismatch")
        require(zlib.crc32(raw) == entry.CRC, "ZIP CRC mismatch")
        require(hashlib.sha256(raw).hexdigest() == expected_sha256, "Source member SHA-256 changed")
        Path(destination).write_bytes(raw)
    return {"url": url, "archive_bytes": total, "member": member,
            "member_sha256": expected_sha256, "member_bytes": len(raw),
            "downloaded_bytes": len(tail) + len(packed), "requests": [tail_meta, packed_meta],
            "full_archive_checksum_verified": False,
            "verification": "ZIP CRC plus pinned SHA-256 of selected original member"}
