#include <stdio.h>
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "driver/gpio.h"
#include "esp_log.h"


void app_main(void)
{
    //Code_generation_section

    while (1){
        vTaskDelay(pdMS_TO_TICKS(1000));
    }
}
