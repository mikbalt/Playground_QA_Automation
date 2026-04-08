import { describe, it, expect } from "vitest";
import { z } from "zod";

// ---------------------------------------------------------------------------
// Schemas
// ---------------------------------------------------------------------------

const ProductSchema = z.object({
  id: z.number(),
  title: z.string(),
  description: z.string(),
  price: z.number(),
  discountPercentage: z.number(),
  rating: z.number(),
  stock: z.number(),
  brand: z.string().optional(),
  category: z.string(),
  thumbnail: z.string(),
  images: z.array(z.string()),
});

type Product = z.infer<typeof ProductSchema>;

const ProductsResponseSchema = z.object({
  products: z.array(ProductSchema),
  total: z.number(),
  skip: z.number(),
  limit: z.number(),
});

type ProductsResponse = z.infer<typeof ProductsResponseSchema>;

// ---------------------------------------------------------------------------
// Constants
// ---------------------------------------------------------------------------

const BASE_URL = "https://dummyjson.com";

// ---------------------------------------------------------------------------
// Tests
// ---------------------------------------------------------------------------

describe("Products API", () => {
  it("should return a valid products response matching the schema", async () => {
    const response = await fetch(`${BASE_URL}/products`);
    expect(response.status).toBe(200);

    const data = await response.json();
    const parsed = ProductsResponseSchema.safeParse(data);

    expect(parsed.success).toBe(true);
    if (parsed.success) {
      expect(parsed.data.products.length).toBeGreaterThan(0);
      expect(parsed.data.total).toBeGreaterThan(0);
    }
  });

  it("should support pagination with limit and skip", async () => {
    const limit = 5;
    const skip = 10;
    const response = await fetch(
      `${BASE_URL}/products?limit=${limit}&skip=${skip}`
    );
    expect(response.status).toBe(200);

    const data: ProductsResponse = await response.json();

    expect(data.products.length).toBe(limit);
    expect(data.skip).toBe(skip);
    expect(data.limit).toBe(limit);
  });

  it("should search products by query string", async () => {
    const query = "phone";
    const response = await fetch(`${BASE_URL}/products/search?q=${query}`);
    expect(response.status).toBe(200);

    const data: ProductsResponse = await response.json();

    expect(data.products.length).toBeGreaterThan(0);
    data.products.forEach((product) => {
      const matchesQuery =
        product.title.toLowerCase().includes(query) ||
        product.description.toLowerCase().includes(query) ||
        product.category.toLowerCase().includes(query);
      expect(matchesQuery).toBe(true);
    });
  });

  it("should return a single product by ID with valid schema", async () => {
    const productId = 1;
    const response = await fetch(`${BASE_URL}/products/${productId}`);
    expect(response.status).toBe(200);

    const data = await response.json();
    const parsed = ProductSchema.safeParse(data);

    expect(parsed.success).toBe(true);
    if (parsed.success) {
      expect(parsed.data.id).toBe(productId);
      expect(parsed.data.title).toBeTruthy();
      expect(parsed.data.price).toBeGreaterThan(0);
    }
  });

  it("should return 404 for a non-existent product ID", async () => {
    const invalidId = 99999;
    const response = await fetch(`${BASE_URL}/products/${invalidId}`);

    expect(response.status).toBe(404);

    const data = await response.json();
    expect(data.message).toBeDefined();
  });
});
