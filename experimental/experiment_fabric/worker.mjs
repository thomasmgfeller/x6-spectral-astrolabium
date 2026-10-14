// Same registered simulation kernel in browser Workers and Node worker_threads.
import {simulate} from './mechanical.mjs';
async function execute(message, send) {
  try { send({ok: true, result: await simulate(message.campaign, message.job, message.truth)}); }
  catch (error) { send({ok: false, error: String(error.message)}); }
}
if (typeof self !== 'undefined' && typeof self.postMessage === 'function') {
  self.onmessage = event => execute(event.data, value => self.postMessage(value));
} else {
  const {parentPort} = await import('node:worker_threads');
  parentPort.on('message', message => execute(message, value => parentPort.postMessage(value)));
}
