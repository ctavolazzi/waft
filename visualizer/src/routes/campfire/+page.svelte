<script lang="ts">
  import { onMount } from 'svelte';
  import axios from 'axios';
  import type { Story } from '../types';

  const API_BASE = 'http://localhost:8000/api';

  let stories: Story[] = [];
  let loading = true;
  let error: string | null = null;
  let showForm = false;
  let newStory = {
    story: '',
    title: '',
    style: 'premium',
    narrative_style: 'medium',
    structure: 'linear',
    include_oracle: true
  };
  let submitting = false;

  interface Story {
    id: string;
    title: string;
    created_at: string;
    pdf_path: string;
    style: string;
    narrative_style: string;
    structure: string;
    oracle_insights?: {
      phase: string;
      coverage: number;
      recommendation?: string;
    };
    preview: string;
    word_count: number;
  }

  onMount(async () => {
    await loadStories();
  });

  async function loadStories() {
    try {
      loading = true;
      error = null;
      const response = await axios.get(`${API_BASE}/campfire/stories`);
      stories = response.data.stories || [];
    } catch (e: any) {
      error = e.response?.data?.detail || e.message || 'Failed to load stories';
      console.error('Error loading stories:', e);
    } finally {
      loading = false;
    }
  }

  async function createStory() {
    if (!newStory.story.trim()) {
      error = 'Story text is required';
      return;
    }

    try {
      submitting = true;
      error = null;
      const response = await axios.post(`${API_BASE}/campfire/stories`, newStory);
      
      // Reset form
      newStory = {
        story: '',
        title: '',
        style: 'premium',
        narrative_style: 'medium',
        structure: 'linear',
        include_oracle: true
      };
      showForm = false;
      
      // Reload stories
      await loadStories();
      
      // Open PDF if available
      if (response.data.pdf_path) {
        window.open(`http://localhost:8000/${response.data.pdf_path}`, '_blank');
      }
    } catch (e: any) {
      error = e.response?.data?.detail || e.message || 'Failed to create story';
      console.error('Error creating story:', e);
    } finally {
      submitting = false;
    }
  }

  function formatDate(dateString: string): string {
    const date = new Date(dateString);
    return date.toLocaleDateString() + ' ' + date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  }

  function openPDF(pdfPath: string) {
    window.open(`http://localhost:8000/${pdfPath}`, '_blank');
  }
</script>

<div class="min-h-screen bg-gradient-to-br from-amber-50 via-orange-50 to-red-50 dark:from-gray-900 dark:via-gray-800 dark:to-gray-900">
  <div class="container mx-auto px-4 py-8 max-w-6xl">
    <!-- Header -->
    <div class="text-center mb-12">
      <h1 class="text-5xl font-bold mb-4 bg-gradient-to-r from-orange-600 to-red-600 bg-clip-text text-transparent">
        🔥 The Campfire
      </h1>
      <p class="text-xl text-gray-600 dark:text-gray-300 mb-6">
        Gather around the campfire to tell stories
      </p>
      <button
        on:click={() => showForm = !showForm}
        class="px-6 py-3 bg-orange-600 hover:bg-orange-700 text-white rounded-lg font-semibold shadow-lg transition-colors"
      >
        {showForm ? 'Cancel' : '+ Tell a Story'}
      </button>
    </div>

    <!-- Error Message -->
    {#if error}
      <div class="mb-6 p-4 bg-red-100 dark:bg-red-900 border border-red-400 dark:border-red-700 text-red-700 dark:text-red-200 rounded-lg">
        {error}
      </div>
    {/if}

    <!-- Story Form -->
    {#if showForm}
      <div class="mb-8 p-6 bg-white dark:bg-gray-800 rounded-lg shadow-xl border border-orange-200 dark:border-gray-700">
        <h2 class="text-2xl font-bold mb-4 text-gray-800 dark:text-gray-200">Tell Your Story</h2>
        
        <div class="space-y-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
              Story Title (optional)
            </label>
            <input
              type="text"
              bind:value={newStory.title}
              placeholder="Auto-generated from first line if empty"
              class="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100"
            />
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
              Your Story *
            </label>
            <textarea
              bind:value={newStory.story}
              placeholder="Once upon a time..."
              rows="10"
              class="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100"
            ></textarea>
          </div>

          <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                PDF Style
              </label>
              <select
                bind:value={newStory.style}
                class="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100"
              >
                <option value="premium">Premium</option>
                <option value="clinical_standard">Clinical Standard</option>
                <option value="professional">Professional</option>
              </select>
            </div>

            <div>
              <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                Narrative Style
              </label>
              <select
                bind:value={newStory.narrative_style}
                class="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100"
              >
                <option value="simple">Simple</option>
                <option value="medium">Medium</option>
              </select>
            </div>

            <div>
              <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                Structure
              </label>
              <select
                bind:value={newStory.structure}
                class="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100"
              >
                <option value="linear">Linear</option>
                <option value="three_act">Three Act</option>
              </select>
            </div>
          </div>

          <div class="flex items-center">
            <input
              type="checkbox"
              bind:checked={newStory.include_oracle}
              id="include_oracle"
              class="mr-2"
            />
            <label for="include_oracle" class="text-sm text-gray-700 dark:text-gray-300">
              Include Oracle insights (requires Empirica)
            </label>
          </div>

          <button
            on:click={createStory}
            disabled={submitting || !newStory.story.trim()}
            class="w-full px-6 py-3 bg-orange-600 hover:bg-orange-700 disabled:bg-gray-400 text-white rounded-lg font-semibold shadow-lg transition-colors"
          >
            {submitting ? 'Telling Story...' : 'Tell Story Around the Campfire'}
          </button>
        </div>
      </div>
    {/if}

    <!-- Stories List -->
    {#if loading}
      <div class="text-center py-12">
        <div class="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-orange-600"></div>
        <p class="mt-4 text-gray-600 dark:text-gray-400">Loading stories...</p>
      </div>
    {:else if stories.length === 0}
      <div class="text-center py-12 bg-white dark:bg-gray-800 rounded-lg shadow-lg border border-orange-200 dark:border-gray-700">
        <p class="text-xl text-gray-600 dark:text-gray-400 mb-4">No stories yet</p>
        <p class="text-gray-500 dark:text-gray-500">Be the first to tell a story around the campfire!</p>
      </div>
    {:else}
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {#each stories as story (story.id)}
          <div class="bg-white dark:bg-gray-800 rounded-lg shadow-lg border border-orange-200 dark:border-gray-700 overflow-hidden hover:shadow-xl transition-shadow">
            <!-- Story Header -->
            <div class="p-6 border-b border-orange-100 dark:border-gray-700">
              <h3 class="text-xl font-bold text-gray-800 dark:text-gray-200 mb-2">
                {story.title}
              </h3>
              <p class="text-sm text-gray-500 dark:text-gray-400">
                {formatDate(story.created_at)}
              </p>
            </div>

            <!-- Story Preview -->
            <div class="p-6">
              <p class="text-gray-700 dark:text-gray-300 mb-4 line-clamp-3">
                {story.preview}
              </p>
              
              <!-- Oracle Insights Badge -->
              {#if story.oracle_insights}
                <div class="mb-4 p-3 bg-purple-50 dark:bg-purple-900/20 rounded-lg border border-purple-200 dark:border-purple-800">
                  <p class="text-xs font-semibold text-purple-700 dark:text-purple-300 mb-1">
                    🔮 Oracle Insights
                  </p>
                  <p class="text-xs text-purple-600 dark:text-purple-400">
                    Phase: {story.oracle_insights.phase} • Coverage: {(story.oracle_insights.coverage * 100).toFixed(0)}%
                  </p>
                </div>
              {/if}

              <!-- Story Metadata -->
              <div class="flex flex-wrap gap-2 mb-4">
                <span class="px-2 py-1 text-xs bg-orange-100 dark:bg-orange-900/30 text-orange-700 dark:text-orange-300 rounded">
                  {story.style}
                </span>
                <span class="px-2 py-1 text-xs bg-blue-100 dark:bg-blue-900/30 text-blue-700 dark:text-blue-300 rounded">
                  {story.narrative_style}
                </span>
                <span class="px-2 py-1 text-xs bg-green-100 dark:bg-green-900/30 text-green-700 dark:text-green-300 rounded">
                  {story.word_count} words
                </span>
              </div>
            </div>

            <!-- Actions -->
            <div class="p-6 pt-0 flex gap-2">
              <button
                on:click={() => openPDF(story.pdf_path)}
                class="flex-1 px-4 py-2 bg-orange-600 hover:bg-orange-700 text-white rounded-lg font-semibold text-sm transition-colors"
              >
                📄 View PDF
              </button>
            </div>
          </div>
        {/each}
      </div>
    {/if}
  </div>
</div>

<style>
  .line-clamp-3 {
    display: -webkit-box;
    -webkit-line-clamp: 3;
    -webkit-box-orient: vertical;
    overflow: hidden;
  }
</style>
