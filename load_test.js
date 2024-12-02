import http from 'k6/http';
import { sleep, check } from 'k6';


let url = __ENV.DEMO_URL || ''

export let options = {
  stages: [
    { duration: '10s', target: 100 },  // Ramp-up to 20 users in 10 seconds
    { duration: '10', target: 100 },   // Hold at 20 users for 1 minute
    { duration: '10s', target: 0 },   // Ramp down to 0 users in 10 seconds
  ],
};

export default function () {

  let res = http.get(url);
  check(res, { 'status was 200': (r) => r.status === 200 });
}
