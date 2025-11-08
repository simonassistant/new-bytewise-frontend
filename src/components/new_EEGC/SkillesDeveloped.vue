<template>
  <div class="md:col-span-2 space-y-6">
    <!-- Skills Dashboard -->
    <div class="grid md:grid-cols-2 gap-6">
      <div class="bg-white p-6 rounded-lg shadow-lg">
        <h2
          class="text-xl font-bold mb-4 bg-gradient-to-r from-purple-400 to-pink-500 bg-clip-text text-transparent"
        >
          Skills Being Developed
        </h2>

        <SkillBadge
          borderColor="border-blue-500"
          title="In-Depth Conversation"
          textColor="text-blue-600"
          :points="[
            'Ask follow-up questions',
            'Engage in multi-level dialogue',
            'Maintain conversation depth',
          ]"
        />
        <SkillBadge
          borderColor="border-purple-500"
          title="Critical Review"
          textColor="text-purple-600"
          :points="[
            'Evaluate AI suggestions critically',
            'Provide evidence-based justification',
            'Accept/reject with reasoning',
          ]"
        />
        <SkillBadge
          borderColor="border-green-500"
          title="Iterative Refinement"
          textColor="text-green-600"
          :points="[
            'Multiple revision cycles',
            'Build on previous feedback',
            'Progressive improvement',
          ]"
        />
      </div>

      <!-- Session Progress -->
      <div class="bg-white p-6 rounded-lg shadow-lg">
        <h2 class="text-xl font-bold mb-4">Session Progress</h2>
        <div class="space-y-3">
          <SessionStat label="Total Exchanges" :value="stats.exchanges" color="blue" />
          <SessionStat label="Follow-up Questions" :value="stats.questions" color="purple" />
          <SessionStat label="Revision Cycles" :value="stats.revisions" color="green" />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, h, defineComponent, reactive } from "vue"

/* ------------ Mock Session Stats ------------ */
const stats = reactive({
  exchanges: 12,
  questions: 4,
  revisions: 3,
})

/* ------------ Components ------------ */
const SkillBadge = defineComponent({
  name: "SkillBadge",
  props: {
    borderColor: { type: String, required: true },
    title: { type: String, required: true },
    textColor: { type: String, required: true },
    points: { type: Array, required: true },
  },
  setup(props) {
    return () =>
      h("div", { class: `border-l-4 pl-4 mb-4 ${props.borderColor}` }, [
        h("h3", { class: `font-semibold ${props.textColor}` }, props.title),
        h(
          "ul",
          { class: "text-sm text-gray-600 mt-1" },
          props.points.map((p, i) => h("li", { key: i }, `• ${p}`))
        ),
      ])
  },
})

const SessionStat = defineComponent({
  name: "SessionStat",
  props: {
    label: { type: String, required: true },
    value: { type: [Number, String], required: true }, // Flexible for both
    color: { type: String, default: "gray" },
  },
  setup(props) {
    const map = {
      blue: "bg-blue-100 text-blue-800",
      purple: "bg-purple-100 text-purple-800",
      green: "bg-green-100 text-green-800",
      gray: "bg-gray-100 text-gray-800",
    }
    const colorClasses = computed(() => map[props.color] || map.gray)

    return () =>
      h("div", { class: "flex justify-between items-center" }, [
        h("span", { class: "text-sm font-medium" }, props.label),
        h(
          "span",
          { class: `px-3 py-1 rounded-full text-sm font-semibold ${colorClasses.value}` },
          props.value
        ),
      ])
  },
})
</script>
