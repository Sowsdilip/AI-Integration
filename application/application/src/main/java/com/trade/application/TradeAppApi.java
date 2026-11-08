package com.trade.application;

import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;

import com.trade.application.TradeApplicationController.LcDetails;

import jakarta.validation.constraints.Pattern;

@RequestMapping("/api")
public interface TradeAppApi {
	
	@GetMapping(value = "/lc/{lcNumber}", produces = "application/json")
	public ResponseEntity<LcDetails> getLcDetails(@PathVariable  @Pattern(regexp = "[A-Za-z0-9-]{3,16}") String lcNumber);

}
