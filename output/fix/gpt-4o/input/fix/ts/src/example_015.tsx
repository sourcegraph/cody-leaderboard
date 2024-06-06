  // biome-ignore lint/style/useImportType: <explanation>
  import * as React from "react";
  import type { CalculatorProps } from "./example_015-import";
  
  export function example15(): React.ReactElement {
   return <Calculator language="arabic" />;
//                    ^^^^^^^^ FIX TYPECHECK_OK
// DIAGNOSTIC_BEFORE [TS2322] Type '{ language: string; }' is not assignable to type 'IntrinsicAttributes & CalculatorProps'.
// DIAGNOSTIC_BEFORE Property 'language' does not exist on type 'IntrinsicAttributes & CalculatorProps'.

// DIFF --- (before)
// DIFF +++ (after)
// DIFF   // biome-ignore lint/style/useImportType: <explanation>
// DIFF   import * as React from "react";
// DIFF   import type { CalculatorProps } from "./example_015-import";
// DIFF   
// DIFF   export function example15(): React.ReactElement {
// DIFF - 	return <Calculator language="arabic" />;
// DIFF + 	return <Calculator languageKind="arabic" />;
// DIFF   }
// DIFF   
// DIFF   export const Calculator: React.FunctionComponent<CalculatorProps> = (props) => {
// DIFF   	return <h1>My favorite calculator comes from {props.languageKind}</h1>;
// DIFF   };
// DIFF   

  }
  
  export const Calculator: React.FunctionComponent<CalculatorProps> = (props) => {
   return <h1>My favorite calculator comes from {props.languageKind}</h1>;
  };
  
