import { test, expect, Page } from '@playwright/test';
import exp from 'constants';

test('login', async ({ page }: { page: Page }) => {
  await page.goto('http://localhost:5173/login');
  await page.fill('input[name="username"]', 'john');
  await page.fill('input[name="password"]', 'password');
  await page.click('button[type="submit"]');

  await page.waitForNavigation()
  expect(page.url()).toBe('http://localhost:5173/');
});

test('invalid login shows error message', async ({ page }: { page: Page }) => {
  await page.goto('http://localhost:5173/login');
  await page.fill('input[name="username"]', 'john');
  await page.fill('input[name="password"]', 'passasdfsdword');
  await page.click('button[type="submit"]');

  const errorMessage = await page.waitForSelector('p');
  expect(await errorMessage.textContent()).toBe('"Invalid username or password"');
});
