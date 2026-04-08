import http from 'k6/http';
import { check, sleep } from 'k6';

export const options = {
  stages: [
    { duration: '30s', target: 10 },  // Ramp up to 10 users
    { duration: '2m', target: 10 },   // Hold at 10 users
    { duration: '30s', target: 0 },   // Ramp down to 0
  ],
  thresholds: {
    http_req_duration: ['p(95)<500'],
    http_req_failed: ['rate<0.01'],
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
    'login returns token': (r) => JSON.parse(r.body).accessToken !== undefined,
  });

  const token = loginRes.json('accessToken');

  sleep(1);

  // Browse products with auth
  const productsRes = http.get(`${BASE_URL}/products?limit=10`, {
    headers: { Authorization: `Bearer ${token}` },
  });

  check(productsRes, {
    'products status is 200': (r) => r.status === 200,
    'products list returned': (r) => JSON.parse(r.body).products.length > 0,
  });

  sleep(1);

  // View a specific product
  const productId = Math.floor(Math.random() * 30) + 1;
  const productRes = http.get(`${BASE_URL}/products/${productId}`, {
    headers: { Authorization: `Bearer ${token}` },
  });

  check(productRes, {
    'product status is 200': (r) => r.status === 200,
    'product has id': (r) => JSON.parse(r.body).id === productId,
  });

  sleep(1);

  // Search products
  const searchRes = http.get(`${BASE_URL}/products/search?q=phone`, {
    headers: { Authorization: `Bearer ${token}` },
  });

  check(searchRes, {
    'search status is 200': (r) => r.status === 200,
    'search returns results': (r) => JSON.parse(r.body).products !== undefined,
  });

  sleep(2);
}
