interface CodeIntelligence {
    symbols: string[]
}

/**
 * Squirrel is a code intelligence API.
 */
interface Squirrel {
    symbolInformation(file: string): CodeIntelligence
}

