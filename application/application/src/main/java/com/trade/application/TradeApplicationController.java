package com.trade.application;

import java.math.BigDecimal;
import java.time.LocalDate;
import java.util.Map;

import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.server.ResponseStatusException;
import org.springframework.http.HttpStatus;

@RestController
public class TradeApplicationController implements TradeAppApi {

	public record LcDetails(String lcNumber, String status, BigDecimal amount, String currency, LocalDate expiryDate,
			String beneficiary) {
	}

	public static final Map<String, LcDetails> LC_DETAILS = Map.of("LC-1001",
			new LcDetails("LC-1001", "ISSUED", new BigDecimal("1000"), "USD", LocalDate.of(2026, 11, 10),
					"Global Trade Solutions LLC"),
			"LC-1002",
			new LcDetails("LC-1002", "EXPIRED", new BigDecimal("3000"), "AED", LocalDate.of(2026, 8, 10),
					"Al Noor International Trading LLC"),
			"LC-1003", new LcDetails("LC-1003", "DOCUMENTS_UNDER_REVIEW", new BigDecimal("30000"), "ZAR",
					LocalDate.of(2030, 1, 20), "Prime Horizon Exports Ltd"));

	@Override
	public ResponseEntity<LcDetails> getLcDetails(String lcNumber) {
		LcDetails lcDetails = LC_DETAILS.get(lcNumber.toUpperCase());
		if (null == lcDetails) {
			throw new ResponseStatusException(HttpStatus.NOT_FOUND,"LC " + lcNumber + " not found");
		}
		return new ResponseEntity<LcDetails>(lcDetails, HttpStatus.OK);
	}

}
