
<template>
  <div class="deployment justify-center ml-[55px] w-screen text-white">
       <div class="deployment-container opponent" style="top: 0%; display: flex;">
            <div class="deployment-zone">
            </div>
            <div class="deployment-zone">
            </div>
            <div class="deployment-zone">
            </div>
        </div>
        <div class="deployment-container playerone" style="top: 0%; display: flex;">
            <div class="deployment-zone">
            </div>
            <div class="deployment-zone">
            </div>
            <div class="deployment-zone">
            </div>
        </div>
    </div>
</template>


<script>
</script>

<style scoped>
.deployment{
    position: absolute;
    width: auto;
    left: 0;
    top: 30%;
}
.deployment-zone{
    display: flex;
    flex-direction: row;
    background-color: transparent;
    height: 165px;
    width: 110px;
    margin-bottom: 10px;
    margin-left: 20px;
    box-shadow: 0px 0px 10px rgba(0, 0, 0, 1);
    border: 1px solid rgba(0, 0, 0, 0.5);
}
</style>