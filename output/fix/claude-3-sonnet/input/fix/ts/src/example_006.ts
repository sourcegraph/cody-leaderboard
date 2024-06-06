  import { type EnglishSpeakingFoodie, foodie } from "./example_005-import";
  
  export function example6(): EnglishSpeakingFoodie {
   return {spanishPotatoes:  foodie.patatasBravadas }
//                                  ^^^^^^^^^^^^^^^ FIX TYPECHECK_OK
// DIAGNOSTIC_BEFORE [TS2551] Property 'patatasBravadas' does not exist on type 'Foodie'. Did you mean 'patatasBravas'?

// DIFF --- (before)
// DIFF +++ (after)
// DIFF   import { type EnglishSpeakingFoodie, foodie } from "./example_005-import";
// DIFF   
// DIFF   export function example6(): EnglishSpeakingFoodie {
// DIFF - 	return {spanishPotatoes:  foodie.patatasBravadas }
// DIFF + 	return {spanishPotatoes: foodie.patatasBravas}
// DIFF   }
// DIFF   

  }
  
