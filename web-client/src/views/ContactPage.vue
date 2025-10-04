<template>
  <div class="page">
    <NavBar />
    <main class="container">
      <section class="wrap">
        <div class="copy">
          <h1>Contact</h1>
          <p>Questions, ideas, collabs, or data tips? Send us a message.</p>

          <form class="form" @submit.prevent="submit">
            <label>
              <span>Name</span>
              <input v-model="form.name" required placeholder="Ada Lovelace" />
            </label>

            <label>
              <span>Email</span>
              <input v-model="form.email" type="email" required placeholder="ada@hivemind.exe" />
            </label>

            <label class="full">
              <span>Message</span>
              <textarea v-model="form.msg" rows="6" required
                placeholder="Tell us how you'd like to use BloomWatch…"></textarea>
            </label>

            <button class="btn" type="submit">Send</button>
          </form>
        </div>

        <aside class="card">
          <img :src="logo" alt="bee logo" />
          <p><strong>hivemind.exe</strong><br/>Göteborg, Sweden</p>
          <p><a href="mailto:team@hivemind.exe">team@hivemind.exe</a></p>
        </aside>
      </section>
    </main>
  </div>
</template>

<script setup>
import { reactive } from 'vue'
import NavBar from '@/components/NavBar.vue'
import logo from '@/assets/hivemind.exe_logo.png'

const form = reactive({ name:'', email:'', msg:'' })
function submit(){
  // placeholder: hook this to your API/email later
  alert(`Thanks, ${form.name}! We'll get back to you at ${form.email}.`)
}
</script>

<style scoped>
.page{ background:#f2f1eb; min-height:100vh; }
.container{ max-width:1100px; margin:0 auto; padding:28px 20px 60px; }
.wrap{ display:grid; grid-template-columns: 1.1fr .9fr; gap:26px; align-items:start; }
.copy h1{ font-size:34px; margin:10px 0 12px; color:#2c2c2c; }

.form{
  display:grid; grid-template-columns: 1fr 1fr; gap:16px; margin-top:12px;
}
.form label{ display:flex; flex-direction:column; gap:6px; }
.form label span{ font-size:14px; color:#4a4a4a; }
.form input, .form textarea{
  background:#fff; border:1px solid #e1e1e1; border-radius:10px;
  padding:12px 14px; font-size:16px; outline:none;
}
.form input:focus, .form textarea:focus{ border-color:#0f1917; box-shadow:0 0 0 3px rgba(15,25,23,.08); }
.full{ grid-column:1 / -1; }
.btn{
  grid-column:1 / -1; justify-self:start;
  background:#0f1917; color:#e8f3ef; border:0; border-radius:12px;
  padding:12px 18px; font-weight:600; cursor:pointer;
}
.btn:hover{ filter:brightness(1.08); }

.card{
  background:#0f1917; color:#e8f3ef; border-radius:14px; padding:22px;
  box-shadow:0 10px 24px rgba(0,0,0,.12);
}
.card img{ width:40px; height:auto; margin-bottom:10px; }
.card a{ color:#b3ffea; }
@media (max-width:900px){
  .wrap{ grid-template-columns:1fr; }
}
</style>
