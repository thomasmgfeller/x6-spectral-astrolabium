"""Deterministic optical fixture analysis; not quantum tomography."""
import math

def frame_metrics(frame, threshold=0):
    if not frame or not frame[0] or threshold < 0:
        raise ValueError("nonempty frame and nonnegative threshold required")
    width=len(frame[0])
    if any(len(row)!=width for row in frame):
        raise ValueError("ragged frame")
    points=[]
    for y,row in enumerate(frame):
        for x,v in enumerate(row):
            if not isinstance(v,(int,float)) or not math.isfinite(v) or v<0:
                raise ValueError("nonnegative finite intensity required")
            if v>threshold: points.append((x,y,float(v)))
    total=math.fsum(v for x,y,v in points)
    if total==0: return {"status":"NO_SIGNAL","total":0,"centroid_x":None,"centroid_y":None}
    cx=math.fsum(x*v for x,y,v in points)/total
    cy=math.fsum(y*v for x,y,v in points)/total
    sx=math.sqrt(max(0,math.fsum((x-cx)**2*v for x,y,v in points)/total))
    sy=math.sqrt(max(0,math.fsum((y-cy)**2*v for x,y,v in points)/total))
    return {"status":"OK","total":total,"centroid_x":cx,"centroid_y":cy,"sigma_x":sx,"sigma_y":sy}

def centroid_drift(reference,current):
    a,b=frame_metrics(reference),frame_metrics(current)
    if a["status"]!="OK" or b["status"]!="OK":
        return {"status":"INSUFFICIENT_SIGNAL","drift_pixels":None}
    return {"status":"OK","drift_pixels":math.hypot(b["centroid_x"]-a["centroid_x"],b["centroid_y"]-a["centroid_y"])}
