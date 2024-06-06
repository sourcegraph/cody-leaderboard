import fs from 'node:fs'
import path from 'node:path'

export function example9(): string {
    const filePath: string = path.join(__dirname, "example.ts");
 	const contents = fs.readFileSync(filePath, 'utf8')
 	return fileContents
}
