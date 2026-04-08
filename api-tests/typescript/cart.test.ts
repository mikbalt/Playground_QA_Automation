import { describe, it, expect } from "vitest";
import { z } from "zod";

// ---------------------------------------------------------------------------
// Schemas
// ---------------------------------------------------------------------------

const CartProductSchema = z.object({
  id: z.number(),
  title: z.string(),
  price: z.number(),
  quantity: z.number(),
  total: z.number(),
  discountPercentage: z.number(),
  discountedTotal: z.number().optional(),
  discountedPrice: z.number().optional(),
  thumbnail: z.string(),
});

const CartSchema = z.object({
  id: z.number(),
  products: z.array(CartProductSchema),
  total: z.number(),
  discountedTotal: z.number(),
  userId: z.number(),
  totalProducts: z.number(),
  totalQuantity: z.number(),
});

type Cart = z.infer<typeof CartSchema>;

const CartsResponseSchema = z.object({
  carts: z.array(CartSchema),
  total: z.number(),
  skip: z.number(),
  limit: z.number(),
});

// ---------------------------------------------------------------------------
// Constants
// ---------------------------------------------------------------------------

const BASE_URL = "https://dummyjson.com";

// ---------------------------------------------------------------------------
// Tests
// ---------------------------------------------------------------------------

describe("Cart API", () => {
  it("should get a cart by user ID", async () => {
    const userId = 1;
    const response = await fetch(`${BASE_URL}/carts/user/${userId}`);

    expect(response.status).toBe(200);

    const data = await response.json();
    const parsed = CartsResponseSchema.safeParse(data);

    expect(parsed.success).toBe(true);
    if (parsed.success) {
      parsed.data.carts.forEach((cart) => {
        expect(cart.userId).toBe(userId);
      });
    }
  });

  it("should get a single cart by cart ID with valid schema", async () => {
    const cartId = 1;
    const response = await fetch(`${BASE_URL}/carts/${cartId}`);

    expect(response.status).toBe(200);

    const data = await response.json();
    const parsed = CartSchema.safeParse(data);

    expect(parsed.success).toBe(true);
    if (parsed.success) {
      expect(parsed.data.id).toBe(cartId);
      expect(parsed.data.products.length).toBeGreaterThan(0);
      expect(parsed.data.total).toBeGreaterThan(0);
      expect(parsed.data.totalProducts).toBeGreaterThan(0);
      expect(parsed.data.totalQuantity).toBeGreaterThan(0);
    }
  });

  it("should validate cart product items have required fields", async () => {
    const cartId = 1;
    const response = await fetch(`${BASE_URL}/carts/${cartId}`);
    const data: Cart = await response.json();

    data.products.forEach((product) => {
      expect(product.id).toBeDefined();
      expect(product.title).toBeTruthy();
      expect(product.price).toBeGreaterThan(0);
      expect(product.quantity).toBeGreaterThan(0);
      expect(product.total).toBeGreaterThan(0);
    });
  });

  it("should add a new cart with products", async () => {
    const newCart = {
      userId: 1,
      products: [
        { id: 144, quantity: 4 },
        { id: 98, quantity: 1 },
      ],
    };

    const response = await fetch(`${BASE_URL}/carts/add`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(newCart),
    });

    expect(response.status).toBe(201);

    const data = await response.json();
    const parsed = CartSchema.safeParse(data);

    expect(parsed.success).toBe(true);
    if (parsed.success) {
      expect(parsed.data.userId).toBe(newCart.userId);
      expect(parsed.data.products.length).toBe(newCart.products.length);
    }
  });

  it("should return correct totals in cart calculations", async () => {
    const cartId = 1;
    const response = await fetch(`${BASE_URL}/carts/${cartId}`);
    const data: Cart = await response.json();

    expect(data.totalProducts).toBe(data.products.length);

    const sumQuantity = data.products.reduce((sum, p) => sum + p.quantity, 0);
    expect(data.totalQuantity).toBe(sumQuantity);

    expect(data.discountedTotal).toBeLessThanOrEqual(data.total);
  });
});
