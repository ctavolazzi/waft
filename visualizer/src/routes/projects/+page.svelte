<script lang="ts">
    import { onMount } from 'svelte';
    import { apiClient } from '$lib/api/client';
    import AppShell from '$lib/components/layout/AppShell.svelte';
    import StatusCard from '$lib/components/cards/StatusCard.svelte';
    import ProgressBar from '$lib/components/status/ProgressBar.svelte';
    import Badge from '$lib/components/status/Badge.svelte';
    export let params: Record<string, string> | undefined = undefined;
    void params;

    interface Project {
        project_id: string;
        title: string;
        description: string;
        status: string;
        progress_percent: number;
        tags: string[];
        milestones: Array<{
            milestone_id: string;
            title: string;
            description: string;
            completed: boolean;
        }>;
        created_at: string;
        updated_at: string;
        related_work_efforts: string[];
    }

    interface Stats {
        total_projects: number;
        active_projects: number;
        avg_progress: number;
        total_milestones: number;
    }

    let projects: Project[] = [];
    let stats: Stats | null = null;
    let loading = true;
    let error: string | null = null;
    let selectedProject: Project | null = null;

    onMount(async () => {
        await loadData();
        // Auto-refresh every 30 seconds
        setInterval(loadData, 30000);
    });

    async function loadData() {
        try {
            loading = true;
            error = null;

            const [projectsData, statsData] = await Promise.all([
                apiClient.get<Project[]>('/api/projects'),
                apiClient.get<Stats>('/api/projects/stats')
            ]);

            projects = projectsData;
            stats = statsData;
        } catch (e) {
            error = e instanceof Error ? e.message : 'Failed to load projects';
            console.error('Error loading projects:', e);
        } finally {
            loading = false;
        }
    }

    function getStatusColor(status: string): string {
        const colors: Record<string, string> = {
            planning: 'blue',
            active: 'green',
            paused: 'yellow',
            completed: 'purple',
            archived: 'gray'
        };
        return colors[status] || 'gray';
    }

    function formatDate(dateString: string): string {
        const date = new Date(dateString);
        return date.toLocaleDateString() + ' ' + date.toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'});
    }

    function openProject(project: Project) {
        selectedProject = project;
    }

    function closeProject() {
        selectedProject = null;
    }
</script>

<AppShell>
    <div class="container mx-auto px-4 py-8">
        <div class="mb-8">
            <h1 class="text-4xl font-bold text-white mb-2">🌊 Projects Dashboard</h1>
            <p class="text-gray-300">Long-Term Project Management System</p>
        </div>

        {#if loading}
            <div class="text-center py-12">
                <div class="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-white"></div>
                <p class="mt-4 text-gray-300">Loading projects...</p>
            </div>
        {:else if error}
            <div class="bg-red-900/50 border border-red-500 rounded-lg p-4 mb-6">
                <p class="text-red-200">❌ Error: {error}</p>
                <button
                    on:click={loadData}
                    class="mt-2 px-4 py-2 bg-red-600 hover:bg-red-700 rounded text-white"
                >
                    Retry
                </button>
            </div>
        {:else}
            <!-- Statistics Cards -->
            {#if stats}
                <div class="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
                    <StatusCard title="Total Projects" value={stats.total_projects.toString()} />
                    <StatusCard title="Active Projects" value={stats.active_projects.toString()} />
                    <StatusCard title="Avg Progress" value={`${stats.avg_progress}%`} />
                    <StatusCard title="Total Milestones" value={stats.total_milestones.toString()} />
                </div>
            {/if}

            <!-- Projects Grid -->
            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {#each projects as project}
                    <div
                        class="bg-gray-800 rounded-lg p-6 hover:bg-gray-750 transition cursor-pointer border border-gray-700"
                        on:click={() => openProject(project)}
                    >
                        <div class="flex justify-between items-start mb-4">
                            <div class="flex-1">
                                <h3 class="text-xl font-bold text-white mb-1">{project.title}</h3>
                                <p class="text-sm text-gray-400 font-mono">{project.project_id}</p>
                            </div>
                            <Badge label={project.status} color={getStatusColor(project.status)} />
                        </div>

                        <div class="mb-4">
                            <div class="flex justify-between text-sm text-gray-400 mb-2">
                                <span>Progress</span>
                                <span>{project.progress_percent.toFixed(1)}%</span>
                            </div>
                            <ProgressBar value={project.progress_percent} max={100} />
                        </div>

                        <div class="grid grid-cols-2 gap-4 text-sm text-gray-400 mb-4">
                            <div>
                                <span class="text-gray-500">📅 Created:</span>
                                <div>{formatDate(project.created_at)}</div>
                            </div>
                            <div>
                                <span class="text-gray-500">🎯 Milestones:</span>
                                <div>
                                    {project.milestones.filter(m => m.completed).length} / {project.milestones.length}
                                </div>
                            </div>
                        </div>

                        {#if project.tags.length > 0}
                            <div class="flex flex-wrap gap-2">
                                {#each project.tags as tag}
                                    <span class="px-2 py-1 bg-gray-700 rounded text-xs text-gray-300">
                                        {tag}
                                    </span>
                                {/each}
                            </div>
                        {/if}
                    </div>
                {/each}
            </div>

            {#if projects.length === 0}
                <div class="text-center py-12 bg-gray-800 rounded-lg border border-gray-700">
                    <p class="text-gray-400 text-lg">No projects found</p>
                    <p class="text-gray-500 text-sm mt-2">Create your first project using: <code class="bg-gray-900 px-2 py-1 rounded">waft project create</code></p>
                </div>
            {/if}
        {/if}
    </div>

    <!-- Project Detail Modal -->
    {#if selectedProject}
        <div
            class="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4"
            on:click={closeProject}
            role="button"
            tabindex="0"
            on:keydown={(e) => e.key === 'Escape' && closeProject()}
        >
            <div
                class="bg-gray-800 rounded-lg max-w-2xl w-full max-h-[90vh] overflow-y-auto border border-gray-700"
                on:click|stopPropagation
            >
                <div class="p-6">
                    <div class="flex justify-between items-start mb-6">
                        <div>
                            <h2 class="text-3xl font-bold text-white mb-2">{selectedProject.title}</h2>
                            <p class="text-sm text-gray-400 font-mono">{selectedProject.project_id}</p>
                        </div>
                        <button
                            on:click={closeProject}
                            class="text-gray-400 hover:text-white text-2xl"
                        >
                            ×
                        </button>
                    </div>

                    <div class="space-y-6">
                        <div>
                            <label class="text-gray-400 text-sm">Status</label>
                            <div class="mt-1">
                                <Badge label={selectedProject.status} color={getStatusColor(selectedProject.status)} />
                            </div>
                        </div>

                        <div>
                            <label class="text-gray-400 text-sm">Progress</label>
                            <div class="mt-2">
                                <ProgressBar value={selectedProject.progress_percent} max={100} />
                                <p class="text-gray-300 mt-1">{selectedProject.progress_percent.toFixed(1)}%</p>
                            </div>
                        </div>

                        {#if selectedProject.description}
                            <div>
                                <label class="text-gray-400 text-sm">Description</label>
                                <p class="text-white mt-1">{selectedProject.description}</p>
                            </div>
                        {/if}

                        {#if selectedProject.milestones.length > 0}
                            <div>
                                <label class="text-gray-400 text-sm">Milestones</label>
                                <div class="mt-2 space-y-2">
                                    {#each selectedProject.milestones as milestone}
                                        <div class="flex items-center gap-3 p-3 bg-gray-700 rounded">
                                            <span class="text-2xl">
                                                {milestone.completed ? '✅' : '⏳'}
                                            </span>
                                            <div class="flex-1">
                                                <p class="text-white font-medium">{milestone.title}</p>
                                                {#if milestone.description}
                                                    <p class="text-gray-400 text-sm mt-1">{milestone.description}</p>
                                                {/if}
                                            </div>
                                        </div>
                                    {/each}
                                </div>
                            </div>
                        {/if}

                        {#if selectedProject.related_work_efforts.length > 0}
                            <div>
                                <label class="text-gray-400 text-sm">Related Work Efforts</label>
                                <div class="mt-2 flex flex-wrap gap-2">
                                    {#each selectedProject.related_work_efforts as we}
                                        <span class="px-3 py-1 bg-gray-700 rounded text-sm text-gray-300">
                                            {we}
                                        </span>
                                    {/each}
                                </div>
                            </div>
                        {/if}

                        <div class="grid grid-cols-2 gap-4 text-sm">
                            <div>
                                <label class="text-gray-400">Created</label>
                                <p class="text-white mt-1">{formatDate(selectedProject.created_at)}</p>
                            </div>
                            <div>
                                <label class="text-gray-400">Updated</label>
                                <p class="text-white mt-1">{formatDate(selectedProject.updated_at)}</p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    {/if}
</AppShell>

<style>
    :global(body) {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        min-height: 100vh;
    }
</style>
