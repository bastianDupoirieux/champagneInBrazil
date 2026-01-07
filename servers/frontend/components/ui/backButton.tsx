import { useRouter } from "next/navigation";

interface BackButtonProps {
    className?: string;
}

export const BackButton = ({className}: BackButtonProps) => {
    const router = useRouter();
    return (
        <button 
            onClick={() => router.back()} 
            className={className} 
            type="button"
        >
            ← back
        </button>
    )
}