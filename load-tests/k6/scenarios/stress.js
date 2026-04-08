import http from 'k6/http';
import { check, sleep } from 'k6';

export const options = {
  stages: [
    { duration: '30s', target: 10 },   // Ramp up to 10 users
    { duration: '1m', target: 10 },    // Hold at 10
    { duration: '30s', target: 50 },   // Ramp up to 50 users
    { duration: '1m', target: 50 },    // Hold at 50
    { duration: '30s', target: 100 },  // Ramp up to 100 users
    { duration: '1m', target: 100 },   // Hold at 100
    { duration: '1m', target: 0 },     // Ramp down to 0
  ],
  thresholds: {
    http_req_duration: ['p(95)<1000', 'p(99)<2000'],
    http_req_failed: ['rate<0.05'],
  },
};

const BASE_URL = 'https://dummyjson.com';

export default function () {
  // Authenticate
  const loginPayload = JSON.stringify({
    username: 'emilys',
    password: 'emilyspass',
  });

  const loginRes = http.post(`${BASE_URL}/auth/login`, loginPayload, {
    headers: { 'Content-Type': 'application/json' },
  });

  check(loginRes, {
    'login status is 200': (r) => r.status === 200,
  });

  sleep(0.5);

  // Browse products
  const productsRes = http.get(`${BASE_URL}/products?limit=10`);

  check(productsRes, {
    'products status is 200': (r) => r.status === 200,
  });

  sleep(0.5);

  // View random product
  const productId = Math.floor(Math.random() * 30) + 1;
  const productRes = http.get(`${BASE_URL}/products/${productId}`);

  check(productRes, {
    'product status is 200': (r) => r.status === 200,
  });

  sleep(0.5);

  // Search products
  const searchTerms = ['phone', 'laptop', 'watch', 'shirt', 'shoes'];
  const term = searchTerms[Math.floor(Math.random() * searchTerms.length)];
  const searchRes = http.get(`${BASE_URL}/products/search?q=${term}`);

  check(searchRes, {
    'search status is 200': (r) => r.status === 200,
  });

  sleep(1);
}
