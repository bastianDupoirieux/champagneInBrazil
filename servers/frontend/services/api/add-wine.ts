import { ApiResponseHandler } from "./api-error-handler";
import type { Wine } from "../../types/wine";

/**
 * Type of form / section we are submitting for.
 * Maps directly to the backend add endpoints defined in `add.py`.
 */
export type FormType =
    | "cellar"
    | "tasted"
    | "wishlist";

/**
 * Payload shape for creating a wine via the add endpoints.
 * This mirrors the shared fields in the backend `WineBase` model,
 * but lets the backend set the in_cellar / has_been_tasted / on_wishlist flags
 * depending on the chosen FormType.
 */
export interface WineFormPayload {
    name: string;
    producer: string;
    region?: string;
    country?: string;
    appellation?: string;
    colour: string;
    vintage?: number;
    notes?: string;
    in_cellar: boolean;
    has_been_tasted: boolean;
    on_wishlist: boolean;
    date_bought?: string;
    price_bought?: number;
    quantity?: number;
}

const endpointMap: Record<FormType, string> = {
    cellar: "/api/add",
    tasted: "/api/add",
    wishlist: "/api/add",
};

/**
 * Post a new wine to the appropriate add endpoint based on formType.
 *
 * - `formType` chooses between `/cellar/add`, `/tasted/add`, `/wishlist/add`
 * - `payload` is serialized as JSON in the request body
 * - Returns the created `Wine` as defined by the backend `WineRead` model
 */
export async function postWineForm(
    formType: FormType,
    payload: WineFormPayload,
    errorMessage?: string,
): Promise<Wine> {
    try {
        const endpoint = endpointMap[formType];
        const response = await fetch(endpoint, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(payload),
        });

        const defaultError =
            errorMessage || `Failed to submit ${formType} wine form.`;

        return await ApiResponseHandler.handleResponse(response, defaultError);
    } catch (error) {
        console.error(`Error posting ${formType} wine form:`, error);
        throw error;
    }
}
