import http from 'k6/http';
import { sleep, check } from 'k6';

export let options = {
  stages: [
    { duration: '10s', target: 500 },  // Ramp-up to 20 users in 10 seconds
    { duration: '10', target: 500 },   // Hold at 20 users for 1 minute
    { duration: '10s', target: 0 },   // Ramp down to 0 users in 10 seconds
  ],
};

export default function () {
  // Send a request to the /cpu_memory1 endpoint
  //let res1 = http.get('http://localhost:5000/cpu_memory1');
  //check(res1, { 'status was 200': (r) => r.status === 200 });
//
  //// Send a request to the /cpu_memory_io2 endpoint
  //let res2 = http.get('http://localhost:5000/cpu_memory_io2');
  //check(res2, { 'status was 200': (r) => r.status === 200 });

  // Send a request to the /cpu_memory_io3 endpoint
  let res3 = http.get('http://localhost:5000/cpu_memory_io3');
  check(res3, { 'status was 200': (r) => r.status === 200 });

  // Sleep to simulate real user think time
  sleep(1);
}
