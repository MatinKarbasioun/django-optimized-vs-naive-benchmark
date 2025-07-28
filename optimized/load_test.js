// k6-load-test.js
import http from 'k6/http';
import { check, group, sleep } from 'k6';
import { Trend } from 'k6/metrics';

// --- Configuration ---
const BASE_URL = __ENV.BASE_URL || 'http://127.0.0.1:8000/api/v1/customers'

// --- Custom Metrics ---
const responseTrend = new Trend('response_time');


export const options = {
  stages: [
    { duration: '30s', target: 50 }, // Ramp-up to 50 users over 30 seconds
    { duration: '1m', target: 50 },  // Stay at 50 users for 1 minute
    { duration: '30s', target: 0 },  // Ramp-down to 0 users
  ],
  // --- Thresholds ---
  thresholds: {
  	'http_req_failed': ['rate<0.01'], // Fail if more than 1% of requests fail
  	'http_req_duration': ['p(95)<1000'], // 95% of requests should be below 1000ms
  	'response_time{scenario:default}': ['p(95)<1000'], // Custom metric check
	  },
};

// --- Main Test Function ---
export default function () {
  group('Customer API Endpoint Load Test', function () {
    // --- 1. Initial List Load (Page 1) ---
    const listRes = http.get(BASE_URL);
    check(listRes, { 'Initial List: status is 200': (r) => r.status === 200 });
    responseTrend.add(listRes.timings.duration);
    sleep(1); // Wait for 1 second between requests

    // --- 2. Filtering ---
    const filterRes = http.get(`${BASE_URL}?first_name=Anthony`);
    check(filterRes, { 'Filtering: status is 200': (r) => r.status === 200 });
    responseTrend.add(filterRes.timings.duration);
    sleep(1);

    // --- 3. Searching ---
    const searchRes = http.get(`${BASE_URL}?search=Nicholas%20Heights`);
    check(searchRes, { 'Searching: status is 200': (r) => r.status === 200 });
    responseTrend.add(searchRes.timings.duration);
    sleep(1);

    // --- 4. Sorting ---
    const sortRes = http.get(`${BASE_URL}?ordering=descending&sort_by=created`);
    check(sortRes, { 'Sorting: status is 200': (r) => r.status === 200 });
    responseTrend.add(sortRes.timings.duration);
    sleep(1);
  });
}