import http from 'k6/http';
import { check, group, sleep } from 'k6';
import { Trend, Rate, Counter } from 'k6/metrics';

// Custom metrics
const loginDuration = new Trend('login_duration');
const browseDuration = new Trend('browse_duration');
const checkoutDuration = new Trend('checkout_duration');
const checkoutSuccessRate = new Rate('checkout_success_rate');
const totalCheckouts = new Counter('total_checkouts');

export const options = {
  stages: [
    { duration: '30s', target: 5 },
    { duration: '2m', target: 10 },
    { duration: '30s', target: 0 },
  ],
  thresholds: {
    http_req_duration: ['p(95)<500'],
    http_req_failed: ['rate<0.01'],
    login_duration: ['p(95)<400'],
    browse_duration: ['p(95)<300'],
    checkout_duration: ['p(95)<600'],
    checkout_success_rate: ['rate>0.95'],
  },
};

const BASE_URL = 'https://dummyjson.com';

export default function () {
  let token;

  // Step 1: Authenticate
  group('01_Authentication', function () {
    const loginPayload = JSON.stringify({
      username: 'emilys',
      password: 'emilyspass',
    });

    const loginRes = http.post(`${BASE_URL}/auth/login`, loginPayload, {
      headers: { 'Content-Type': 'application/json' },
    });

    loginDuration.add(loginRes.timings.duration);

    check(loginRes, {
      'login successful': (r) => r.status === 200,
      'token received': (r) => JSON.parse(r.body).accessToken !== undefined,
    });

    token = loginRes.json('accessToken');
  });

  sleep(1);

  // Step 2: Browse products
  group('02_Browse_Products', function () {
    const headers = { Authorization: `Bearer ${token}` };

    const productsRes = http.get(`${BASE_URL}/products?limit=10`, { headers });
    browseDuration.add(productsRes.timings.duration);

    check(productsRes, {
      'products loaded': (r) => r.status === 200,
      'products not empty': (r) => JSON.parse(r.body).products.length > 0,
    });

    // View a specific product detail
    const productId = Math.floor(Math.random() * 10) + 1;
    const detailRes = http.get(`${BASE_URL}/products/${productId}`, { headers });

    check(detailRes, {
      'product detail loaded': (r) => r.status === 200,
    });
  });

  sleep(1);

  // Step 3: Add to cart
  group('03_Add_To_Cart', function () {
    const headers = {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${token}`,
    };

    const cartPayload = JSON.stringify({
      userId: 1,
      products: [
        { id: 1, quantity: 2 },
        { id: 50, quantity: 1 },
      ],
    });

    const cartRes = http.post(`${BASE_URL}/carts/add`, cartPayload, { headers });

    check(cartRes, {
      'cart created': (r) => r.status === 200 || r.status === 201,
      'cart has products': (r) => JSON.parse(r.body).products.length > 0,
    });
  });

  sleep(1);

  // Step 4: Checkout (simulated via cart update)
  group('04_Checkout', function () {
    const headers = {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${token}`,
    };

    const checkoutPayload = JSON.stringify({
      merge: false,
      products: [
        { id: 1, quantity: 1 },
      ],
    });

    const checkoutRes = http.put(`${BASE_URL}/carts/1`, checkoutPayload, { headers });
    checkoutDuration.add(checkoutRes.timings.duration);
    totalCheckouts.add(1);

    const success = checkoutRes.status === 200;
    checkoutSuccessRate.add(success);

    check(checkoutRes, {
      'checkout status is 200': (r) => r.status === 200,
      'checkout returns cart': (r) => JSON.parse(r.body).products !== undefined,
    });
  });

  sleep(2);
}
