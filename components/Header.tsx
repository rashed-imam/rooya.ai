import Link from 'next/link';
import { useState } from 'react';

export default function Header() {
    const [searchQuery, setSearchQuery] = useState('');

    const handleSearchChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        setSearchQuery(e.target.value);
    };

    const handleSearchSubmit = (e: React.FormEvent) => {
        e.preventDefault();
        // Implement search functionality here
        console.log('Searching for:', searchQuery);
    };

    return (
        <header className="header">
            <div className="logo">
                <Link href="/">
                    <a>Ecom</a>
                </Link>
            </div>
            <nav>
                <ul>
                    <li><Link href="/products"><a>Products</a></Link></li>
                    <li><Link href="/orders"><a>Orders</a></Link></li>
                    <li><Link href="/profile"><a>Profile</a></Link></li>
                </ul>
            </nav>
            <form onSubmit={handleSearchSubmit} className="search-form">
                <input
                    type="text"
                    placeholder="Search products..."
                    value={searchQuery}
                    onChange={handleSearchChange}
                />
                <button type="submit">Search</button>
            </form>
            <div className="login-button">
                <Link href="/login">
                    <a>Login</a>
                </Link>
            </div>
        </header>
    );
} 