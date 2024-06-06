// biome-ignore lint/style/useImportType: <explanation>
import * as React from "react";
import type { CalculatorProps } from "./example_015-import";

export function example15(): React.ReactElement {
	return <Calculator language="arabic" />;
}

export const Calculator: React.FunctionComponent<CalculatorProps> = (props) => {
	return <h1>My favorite calculator comes from {props.languageKind}</h1>;
};
