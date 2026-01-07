interface ErrorProps {
    error: string;
    className?: string;
}

export const Error = ({error, className}: ErrorProps) => {
    return (
        <div className={className}>
            <p className="error-message">{error}</p>
        </div>
    )
}
