import { describe, it, expect } from "vitest";
import { z } from "zod";

// ---------------------------------------------------------------------------
// Schemas
// ---------------------------------------------------------------------------

const LoginResponseSchema = z.object({
  id: z.number(),
  username: z.string(),
  email: z.string(),
  firstName: z.string(),
  lastName: z.string(),
  gender: z.string(),
  image: z.string(),
  accessToken: z.string(),
  refreshToken: z.string(),
});

type LoginResponse = z.infer<typeof LoginResponseSchema>;

// ---------------------------------------------------------------------------
// Constants
// ---------------------------------------------------------------------------

const BASE_URL = "https://dummyjson.com";

const VALID_CREDENTIALS = {
  username: "emilys",
  password: "emilyspass",
};

// ---------------------------------------------------------------------------
// Tests
// ---------------------------------------------------------------------------

describe("Auth API", () => {
  it("should login successfully with valid credentials", async () => {
    const response = await fetch(`${BASE_URL}/auth/login`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(VALID_CREDENTIALS),
    });

    expect(response.status).toBe(200);

    const data: LoginResponse = await response.json();

    expect(data.username).toBe(VALID_CREDENTIALS.username);
    expect(data.firstName).toBeTruthy();
    expect(data.lastName).toBeTruthy();
  });

  it("should return a valid response matching the LoginResponseSchema", async () => {
    const response = await fetch(`${BASE_URL}/auth/login`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(VALID_CREDENTIALS),
    });

    const data = await response.json();
    const parsed = LoginResponseSchema.safeParse(data);

    expect(parsed.success).toBe(true);
  });

  it("should include a non-empty token in the login response", async () => {
    const response = await fetch(`${BASE_URL}/auth/login`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(VALID_CREDENTIALS),
    });

    expect(response.status).toBe(200);

    const data: LoginResponse = await response.json();

    expect(data.accessToken).toBeDefined();
    expect(data.accessToken.length).toBeGreaterThan(0);
    expect(data.refreshToken).toBeDefined();
    expect(data.refreshToken.length).toBeGreaterThan(0);
  });

  it("should reject login with invalid credentials", async () => {
    const response = await fetch(`${BASE_URL}/auth/login`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        username: "invaliduser",
        password: "wrongpassword",
      }),
    });

    expect(response.status).toBe(400);

    const data = await response.json();
    expect(data.message).toBeDefined();
  });

  it("should reject login with missing password", async () => {
    const response = await fetch(`${BASE_URL}/auth/login`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        username: "emilys",
      }),
    });

    expect(response.status).toBe(400);

    const data = await response.json();
    expect(data.message).toBeDefined();
  });
});
