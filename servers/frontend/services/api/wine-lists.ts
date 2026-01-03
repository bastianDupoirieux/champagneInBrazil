import { ApiResponseHandler } from "./api-error-handler";
import type { Wine } from "../../types/wine";

export type WineListType =
    | "cellar" // All wines from cellar
    | "cellar/current" // Wines currently in cellar
    | "cellar/past" // Past wines from the cellar
    | "tasted" // Wines that have been tasted
    | "wishlist"; // Wines on the wishlist

const endpointMap: Record<WineListType, string> = {
    "cellar": "/overview/cellar",
    "cellar/current": "/overview/cellar/current",
    "cellar/past": "/overview/cellar/past",
    "tasted": "/overview/tasted",
    "wishlist": "/overview/wishlist",
};

export async function fetchWinesList(listType: WineListType, errorMessage?: string): Promise<Wine[]>{
    try {
        const endpoint = endpointMap[listType];
        const response = await fetch(endpoint,
            {
                method: "GET",
            }
        );

        if (response.status == 404) {
            console.log(`No wines found for ${listType}`);
            return [];
        }

        const defaultError = errorMessage || `Failed to fetch ${listType} wines`;
        return await ApiResponseHandler.handleResponse(response, defaultError);
    } catch (error) {
        console.error(`Error fetching ${listType} wines:`, error);
        throw error;
    }
}

export async function fetchWinesInCellar(): Promise<Wine[]> {
    return fetchWinesList("cellar", "Failed to fetch wines in cellar")
}

export async function fetchCurrentWinesInCellar(): Promise<Wine[]> {
    return fetchWinesList("cellar/current", "Failed to fetch current wines in cellar")
}

export async function fetchPastWinesFromCellar(): Promise<Wine[]> {
    return fetchWinesList("cellar/past", "Failed to fetch past wines from cellar")
}

export async function fetchTastedWines(): Promise<Wine[]> {
    return fetchWinesList("tasted", "Failed to fetch tasted wines")
}

export async function fetchWinesOnWishlist(): Promise<Wine[]> {
    return fetchWinesList("wishlist", "Failed to fetch wines on wishlist")
}
