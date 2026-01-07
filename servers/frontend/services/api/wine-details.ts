import { ApiResponseHandler } from "./api-error-handler";
import type { Wine } from "../../types/wine";
import { normaliseId } from "../../utils/ids";

const endpoint = "/api/wine/{wine_id}/details";

export async function fetchWineDetails(wineId: string, errorMessage?: string): Promise<Wine | null> {
    const normalisedWineId = normaliseId(wineId);
    try {
        const response = await fetch(endpoint.replace("{wine_id}", normalisedWineId), 
        {
            method: "GET"
        }
    );

    if (response.status == 404) {
        console.log(`Wine details not found for wine with ID ${normalisedWineId}`);
        return null;
    }
    const defaultError = errorMessage || `Failed to fetch wine details for wine with ID ${wineId}`;
    return await ApiResponseHandler.handleResponse(response, defaultError);
    } catch (error) {
        console.error(`Error fetching wine details for wine with ID ${normalisedWineId}:`, error);
        throw error;
    }
}
