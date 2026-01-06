export function defaultValueTupleByState(currentState:string | null): [boolean, boolean, boolean] {
    let defaultVals: [boolean, boolean, boolean];
    if (currentState == "cellar") {
        defaultVals = [true, false, false];
    } else if (currentState == "tasted") {
        defaultVals = [false, true, false];
    } else {
        defaultVals = [false, false, true]
    }
    
    return defaultVals
}
