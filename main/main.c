#include <stdio.h>
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "driver/gpio.h"
#include "esp_log.h"


void app_main(void)
{
    gpio_set_direction(18, OUTPUT);gpio_set_level(18, 1);
    gpio_set_direction(22, OUTPUT);gpio_set_level(22, 0);
    gpio_set_direction(10, OUTPUT);gpio_set_level(10, 1);
    gpio_set_direction(12, OUTPUT);gpio_set_level(12, 1);

    while (1){
        vTaskDelay(pdMS_TO_TICKS(1000));
    }
}
