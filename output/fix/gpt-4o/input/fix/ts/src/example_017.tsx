  // biome-ignore lint/style/useImportType: <explanation>
  import * as React from "react";
  import { Calculator } from "./example_015";
  
  export function example17(lingua?: 'japanese'): React.ReactElement {
   return <Calculator languageKind={} />;
//                                 ^^ FIX TYPECHECK_OK
// DIAGNOSTIC_BEFORE [TS17000] JSX attributes must only be assigned a non-empty 'expression'.

// DIFF --- (before)
// DIFF +++ (after)
// DIFF   // biome-ignore lint/style/useImportType: <explanation>
// DIFF   import * as React from "react";
// DIFF   import { Calculator } from "./example_015";
// DIFF   
// DIFF   export function example17(lingua?: 'japanese'): React.ReactElement {
// DIFF - 	return <Calculator languageKind={} />;
// DIFF + 	return <Calculator languageKind={lingua === 'japanese' ? 'japanese' : undefined} />;
// DIFF   }
// DIFF   
// DIFF   

  }
  
  
