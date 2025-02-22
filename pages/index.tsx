import Header from '@/components/Header';
import Banner from '@/components/Banner';
import ProductsGrid from '@/components/ProductsGrid';
import Footer from '@/components/Footer';
import styles from '../styles/Home.module.css';

export default function Home() {
    return (
        <div className={styles.container}>
            <Header />
            <Banner />
            <main>
                <h2>Our Products</h2>
                <ProductsGrid />
            </main>
            <Footer />
        </div>
    );
} 