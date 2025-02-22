import products from '../todo/products.json';

interface Product {
    sku: number;
    price: number;
}

export default function ProductsGrid() {
    return (
        <div className="products-grid">
            {products.map((product: Product) => (
                <div key={product.sku} className="product-card">
                    <h3>Product SKU: {product.sku}</h3>
                    <p>Price: ${product.price.toFixed(2)}</p>
                    {/* Future Enhancement: Add buttons for actions like Add to Cart */}
                </div>
            ))}
        </div>
    );
} 