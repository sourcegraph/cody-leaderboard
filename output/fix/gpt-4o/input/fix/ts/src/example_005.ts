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
// DIFF + 	return {
// DIFF +     spanishOmelet: foodie.spanishOmelet,
// DIFF +     tacoTruckTacos: foodie.tacoTruckTacos
// DIFF +   }
// DIFF   }
// DIFF   

// DIAGNOSTIC_AFTER [TS2353] Object literal may only specify known properties, and 'spanishOmelet' does not exist in type 'EnglishSpeakingFoodie'.
// DIAGNOSTIC_AFTER [TS2339] Property 'spanishOmelet' does not exist on type 'Foodie'.
// DIAGNOSTIC_AFTER [TS2339] Property 'tacoTruckTacos' does not exist on type 'Foodie'.

  }
  
