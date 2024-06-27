import {sub} from './sub'
import { describe, it, expect } from 'vitest'

describe('sub', () => {
  it('should subtract two numbers', () => {
    expect(sub(1, 2)).toBe(-1);
  });
});