export interface Wine {
    id: string;
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
