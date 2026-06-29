<!--
  Copyright 2025–2026 Guglielmo Celata

  Licensed under the Apache License, Version 2.0 (the "License");
  you may not use this file except in compliance with the License.
  You may obtain a copy of the License at

      http://www.apache.org/licenses/LICENSE-2.0

  Unless required by applicable law or agreed to in writing, software
  distributed under the License is distributed on an "AS IS" BASIS,
  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
  See the License for the specific language governing permissions and
  limitations under the License.
-->

<template>
  <nav class="breadcrumb" aria-label="breadcrumb">
    <ol>
      <li v-for="(crumb, index) in crumbs" :key="index">
        <a v-if="crumb.href" :href="crumb.href">{{ crumb.label }}</a>
        <span v-else class="current">{{ crumb.label }}</span>
        <span v-if="index < crumbs.length - 1" class="separator">›</span>
      </li>
    </ol>
  </nav>
</template>

<script setup lang="ts">
export interface Crumb {
  label: string;
  href?: string;
}

interface Props {
  crumbs: Crumb[];
}

defineProps<Props>();
</script>

<style scoped>
.breadcrumb {
  background-color: rgba(255, 255, 255, 0.9);
  padding: 12px 20px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  margin-bottom: 20px;
}

.breadcrumb ol {
  list-style: none;
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  align-items: center;
  margin: 0;
  padding: 0;
}

.breadcrumb li {
  display: flex;
  align-items: center;
  gap: 8px;
}

.breadcrumb a {
  color: #667eea;
  text-decoration: none;
  font-weight: 500;
  transition: color 0.2s;
}

.breadcrumb a:hover {
  color: #764ba2;
  text-decoration: underline;
}

.breadcrumb .current {
  color: #7f8c8d;
  font-weight: 600;
}

.breadcrumb .separator {
  color: #bdc3c7;
  font-weight: 300;
  user-select: none;
}

@media (max-width: 767px) {
  .breadcrumb {
    padding: 10px 15px;
    font-size: 0.9em;
  }
}
</style>
