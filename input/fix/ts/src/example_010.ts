import fs from 'node:fs'
import path from 'node:path'

export function example10(): string {
    const filePath: string = path.join(__dirname, "example.ts");
 	const fileContents = 42
 	return fileContents
}
