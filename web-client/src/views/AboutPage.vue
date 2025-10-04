<template>
  <div class="page">

    <main class="container">
      <section class="about">
        <div class="copy">
            <h1>About Us</h1>
            <p>
            We are <strong>Flower Power Tower Girls</strong> – a small but mighty team of three software engineers who came together for the NASA Space Apps Challenge 2025. Our project, <em>hivemind.exe</em>, was born from a shared love of bees and the rhythms of plants. Bees follow the pulse of flowers across ecosystems; with NASA Earth observations, we aim to help everyone witness that same pulse on Earth.
            </p>

            <p>
            That idea became the <strong>Bloom Wave Visualizer</strong>, our submission to the challenge
            “BloomWatch: An Earth Observation Application for Global Flowering Phenology.” It transforms NASA’s data into a living story:
            </p>

            <ul>
            <li><strong>Animated 3D globe</strong> where blooming events appear as colorful waves pulsing across continents.</li>
            <li><strong>Seasonal transitions</strong> that show spring “flowing” northward in the Northern Hemisphere (and southward in the Southern).</li>
            <li><strong>Regional signatures</strong> like the dramatic greening of the Sahel during the monsoon season.</li>
            <li><strong>Long-term change</strong> revealing how climate shifts alter bloom timing around the world.</li>
            </ul>

            <p>
            Our vision is more than visualization. We’re building a tool that scientists, farmers, policymakers, and curious minds can use to monitor, predict, and manage vegetation patterns—helping us all stay in tune with the planet’s rhythms.
            </p>

            <p>
            At heart, our project is about curiosity, collaboration, and creativity – and a little bit of flower power. 🌸🐝
            </p>

        </div>

        <figure class="art" aria-label="Flower Power Tower Girls illustration">
            <img :src="artImg" alt="Flower Power Tower Girls illustration" />
        </figure>

      </section>
    </main>
  </div>
</template>

<script setup>
    import artImg from '@/assets/FPTG.png'
</script>


<style scoped>
.page{ background:#f2f1eb; min-height:100vh; }
.container{ max-width:1100px; margin:0 auto; padding:28px 20px 60px; }
.about{
  display:grid; grid-template-columns: 1.2fr 1fr; gap:26px; align-items:start;
}
.copy h1{
  font-family: "Helvetica Neue", Helvetica, Arial, ui-sans-serif, system-ui;
  font-size:38px; margin:12px 0 14px; color:#2c2c2c;
}
.copy p{ color:#3b3b3b; line-height:1.7; }
.copy ul{ margin:10px 0 0 18px; color:#3b3b3b; }
.copy li{ margin:6px 0; }
.art{
  width:100%;
  height:460px;               /* same box height as before */
  border-radius:10px;
}
.art img{
  width:100%;
  height:100%;
  object-fit:contain;         /* shows the whole image, no crop */
  display:block;
}

@media (max-width:900px){
  .about{ grid-template-columns:1fr; }
  .art{ order:-1; height:220px; }
}

</style>
