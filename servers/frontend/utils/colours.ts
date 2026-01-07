export function normaliseColour(colour: string): string {
    return colour
        .toLowerCase()
        .trim()
        .normalize("NFD")
        .replace(/[\u0300-\u036f]/g, '')
        .replace(/\s+/g, '-');
}

export function mapImageToColour(colour: string): string {
    const normalisedColour = normaliseColour(colour);
    const colourMap: Record<string, string> = {
        "red": "/red.svg",
        "white": "/white.svg",
        "rose": "/rose.svg",
        "orange": "/orange.svg",
        "sparkling": "/sparkling.svg"
    };
    return colourMap[normalisedColour] || "/bottle.svg";
}
