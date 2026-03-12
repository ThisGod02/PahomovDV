import { notFound } from 'next/navigation'
import { blogPosts } from '../data'
import Link from 'next/link'

// Функция для генерации статических путей
export async function generateStaticParams() {
    return blogPosts.map((post) => ({
        slug: post.slug,
    }))
}

export default async function BlogPostPage({
    params,
}: {
    params: Promise<{ slug: string }>
}) {
    const { slug } = await params;
    const post = blogPosts.find(p => p.slug === slug)

    if (!post) {
        notFound()
    }

    return (
        <article className="max-w-3xl mx-auto py-12 px-4">
            <header className="mb-10 text-center">
                <Link href="/blog" className="inline-flex items-center gap-2 text-sm font-bold text-blue-600 mb-6 hover:text-blue-700 uppercase tracking-widest transition-colors">
                    <span>←</span> Назад в блог
                </Link>
                <h1 className="text-4xl sm:text-5xl font-extrabold text-gray-900 mb-6 leading-tight">
                    {post.title}
                </h1>
                <div className="flex justify-center items-center gap-4 text-gray-500 font-medium">
                    <time className="flex items-center gap-1">🗓 {post.date}</time>
                    <span className="h-1 w-1 bg-gray-300 rounded-full"></span>
                    <span className="flex items-center gap-1">👤 {post.author}</span>
                </div>
            </header>

            <div className="prose prose-blue lg:prose-xl max-w-none text-gray-700 leading-relaxed">
                <p className="text-xl font-medium text-gray-900 mb-8 border-l-4 border-blue-500 pl-6 italic">
                    {post.excerpt}
                </p>
                <div className="whitespace-pre-line space-y-6">
                    {post.content}
                </div>
            </div>

            <footer className="mt-16 pt-8 border-t border-gray-100">
                <div className="bg-blue-50 p-8 rounded-3xl flex flex-col sm:flex-row items-center justify-between gap-6">
                    <div>
                        <h3 className="text-xl font-bold text-gray-900 mb-2">Понравилась статья?</h3>
                        <p className="text-gray-600">Подписывайтесь на обновления, чтобы не пропустить новые материалы.</p>
                    </div>
                    <button className="whitespace-nowrap bg-blue-600 text-white px-8 py-3 rounded-2xl font-bold hover:bg-blue-700 transition shadow-md">
                        Подписаться
                    </button>
                </div>
            </footer>
        </article>
    )
}
