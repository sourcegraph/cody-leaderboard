import path from 'node:path'

export function example7(): string {
	return path.resolved(process.cwd(), 'example_007.ts') 
}
