  import { type EnglishSpeakingFoodie, foodie } from "./example_005-import";
  
  export function example5(): EnglishSpeakingFoodie {
   return {spanishPotatoes:  foodie.spanishPotatoes }
//                                  ^^^^^^^^^^^^^^^ FIX TYPECHECK_ERROR
// DIAGNOSTIC_BEFORE [TS2339] Property 'spanishPotatoes' does not exist on type 'Foodie'.

// DIFF --- (before)
// DIFF +++ (after)
// DIFF   import { type EnglishSpeakingFoodie, foodie } from "./example_005-import";
// DIFF   
// DIFF   export function example5(): EnglishSpeakingFoodie {
// DIFF - 	return {spanishPotatoes:  foodie.spanishPotatoes }
// DIFF + 	return { ...foodie, spanishPotatoes: foodie.spanishOmelette }
// DIFF   }
// DIFF   

// DIAGNOSTIC_AFTER [TS2339] Property 'spanishOmelette' does not exist on type 'Foodie'.

  }
  
