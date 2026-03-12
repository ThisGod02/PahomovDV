interface ProjectCardProps {
    title: string
    description: string
    technologies: string[]
    link?: string
}

export default function ProjectCard({
    title,
    description,
    technologies,
    link
}: ProjectCardProps) {
    return (
        <div className="group flex flex-col bg-white border border-gray-100 rounded-3xl p-8 shadow-sm hover:shadow-xl transition-all duration-500 transform hover:-translate-y-2">
            <div className="flex-grow">
                <div className="h-12 w-12 bg-blue-50 text-blue-600 rounded-xl flex items-center justify-center mb-6 text-2xl group-hover:scale-110 transition-transform">
                    📁
                </div>
                <h3 className="text-2xl font-bold mb-4 text-gray-900 group-hover:text-blue-600 transition-colors">{title}</h3>
                <p className="text-gray-600 leading-relaxed mb-6">{description}</p>

                <div className="flex flex-wrap gap-2 mb-8">
                    {technologies.map((tech, index) => (
                        <span
                            key={index}
                            className="px-3 py-1 bg-gray-50 text-gray-600 text-xs font-bold rounded-full border border-gray-200 uppercase tracking-tighter"
                        >
                            {tech}
                        </span>
                    ))}
                </div>
            </div>

            {link && (
                <a
                    href={link}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="inline-flex items-center gap-2 text-blue-600 font-bold hover:text-blue-700 transition-all group/link"
                >
                    Посмотреть проект <span className="group-hover/link:translate-x-1 transition-transform">→</span>
                </a>
            )}
        </div>
    )
}
