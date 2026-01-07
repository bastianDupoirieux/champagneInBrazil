interface LoaderProps {
    message?: string;
    className?: string;
}

export const Loader = ({message, className}: LoaderProps) => {
    return (
        <div className={className}>
            {message && <p className="loader-message">{message}</p>}
            <div className="loader-spinner"></div>
        </div>
    )
}
