interface Summer {
  bananas: number
  motorcycles: string[]
}
export function sum(a: number, summer: Summer): number {
  return a + summer.bananas + summer.motorcycles.length
}
