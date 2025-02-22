export default function Footer() {
    return (
        <footer className="footer">
            <p>&copy; {new Date().getFullYear()} Ecom. All rights reserved.</p>
            <ul>
                <li><a href="/about">About Us</a></li>
                <li><a href="/contact">Contact</a></li>
                <li><a href="/terms">Terms of Service</a></li>
            </ul>
        </footer>
    );
} 