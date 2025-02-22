import { useEffect, useState } from 'react';

interface Discount {
    key: string;
    value: number;
}

export default function Banner() {
    const [currentDiscount, setCurrentDiscount] = useState<Discount | null>(null);

    useEffect(() => {
        // Dynamically import discounts.json
        const fetchDiscounts = async () => {
            try {
                const discounts = (await import('../todo/discounts.json')).default;
                if (discounts.length > 0) {
                    const randomIndex = Math.floor(Math.random() * discounts.length);
                    setCurrentDiscount(discounts[randomIndex]);
                }
            } catch (error) {
                console.error("Failed to load discounts:", error);
                setCurrentDiscount(null); // Set to null in case of error
            }
        };

        fetchDiscounts();
    }, []);

    return (
        <div className="banner">
            {currentDiscount ? (
                <p>
                    Use code <strong>{currentDiscount.key}</strong> for a{' '}
                    {currentDiscount.value * 100}% discount!
                </p>
            ) : (
                <p>Welcome to Ecom! Check out our latest products.</p>
            )}
        </div>
    );
}