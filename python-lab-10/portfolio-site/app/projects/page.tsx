import ProjectCard from '../components/ProjectCard'

const projects = [
    {
        title: 'Интернет-магазин электроники',
        description: 'Полнофункциональный интернет-магазин с корзиной, списком желаемого и интеграцией платежной системы Stripe. Полностью адаптивный дизайн.',
        technologies: ['Next.js', 'TypeScript', 'Stripe', 'Tailwind', 'Prisma'],
        link: 'https://example-shop.com'
    },
    {
        title: 'Система управления задачами',
        description: 'Канбан-доска для командной работы с возможностью назначения исполнителей, установки дедлайнов и real-time чатом на WebSockets.',
        technologies: ['React', 'Node.js', 'Socket.io', 'MongoDB'],
        link: 'https://example-tasks.com'
    },
    {
        title: 'Бот для крипто-биржи',
        description: 'Автоматизированная торговая система, использующая API Binance для выполнения сделок по заданным стратегиям и анализа графиков.',
        technologies: ['Python', 'Pandas', 'Ccxt', 'Docker'],
        link: 'https://github.com/example/crypto-bot'
    },
    {
        title: 'Портфолио фотографа',
        description: 'Галерея с ленивой загрузкой изображений, поддержкой фильтров и формой обратной связи. Оптимизировано для SEO и быстрой загрузки.',
        technologies: ['Next.js', 'Framer Motion', 'Cloudinary', 'EmailJS'],
        link: 'https://example-photo.com'
    }
]

export default function ProjectsPage() {
    return (
        <div className="max-w-6xl mx-auto py-10 px-4">
            <div className="mb-12 text-center">
                <h1 className="text-4xl font-extrabold text-gray-900 border-b-4 border-blue-500 inline-block pb-2 mb-4">Мои проекты</h1>
                <p className="text-gray-600 mt-4 text-lg">Коллекция моих работ, от небольших утилит до сложных веб-сервисов.</p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                {projects.map((project, index) => (
                    <ProjectCard
                        key={index}
                        title={project.title}
                        description={project.description}
                        technologies={project.technologies}
                        link={project.link}
                    />
                ))}
            </div>
        </div>
    )
}
