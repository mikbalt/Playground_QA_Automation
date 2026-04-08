import http from 'k6/http';
import { check, sleep } from 'k6';

export const options = {
  vus: 1,
  duration: '1m',
  thresholds: {
    http_req_duration: ['p(95)<500'],
    http_req_failed: ['rate<0.01'],
  },
};

const BASE_URL = 'https://dummyjson.com';

export default function () {
  // Test authentication endpoint
  const loginPayload = JSON.stringify({
    username: 'emilys',
    password: 'emilyspass',
  });

  const loginRes = http.post(`${BASE_URL}/auth/login`, loginPayload, {
    headers: { 'Content-Type': 'application/json' },
  });

  check(loginRes, {
    'login status is 200': (r) => r.status === 200,
    'login returns token': (r) => JSON.parse(r.body).accessToken !== undefined,
  });

  sleep(1);

  // Test products endpoint
  const productsRes = http.get(`${BASE_URL}/products?limit=10`);

  check(productsRes, {
    'products status is 200': (r) => r.status === 200,
    'products returns data': (r) => JSON.parse(r.body).products.length > 0,
  });

  sleep(1);

  // Test single product endpoint
  const productRes = http.get(`${BASE_URL}/products/1`);

  check(productRes, {
    'product status is 200': (r) => r.status === 200,
    'product has title': (r) => JSON.parse(r.body).title !== undefined,
  });

  sleep(1);
}
