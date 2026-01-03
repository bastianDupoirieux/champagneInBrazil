import { v4 as uuidv4 } from "uuid";

export interface Wine {
    id: typeof uuidv4;
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
    quantity?: number
}
