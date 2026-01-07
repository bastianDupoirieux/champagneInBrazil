import { ApiResponseHandler } from "./api-error-handler";
import type { Wine } from "../../types/wine";

const endpoint = "/api/wine/{wine_id}/details";

export async function fetchWineDetails(wineId: string, errorMessage?: string): Promise<Wine | null> {
    try {
        const response = await fetch(endpoint.replace("{wine_id}", wineId), 
        {
            method: "GET"
        }
    );

    if (response.status == 404) {
        console.log(`Wine details not found for wine with ID ${wineId}`);
        return null;
    }
    const defaultError = errorMessage || `Failed to fetch wine details for wine with ID ${wineId}`;
    return await ApiResponseHandler.handleResponse(response, defaultError);
    } catch (error) {
        console.error(`Error fetching wine details for wine with ID ${wineId}:`, error);
        throw error;
    }
}
